import { useEffect, useState } from "react";
import { createDevice, deleteDevice, listDevices } from "./api";
import type { Device } from "./api";

export default function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [error, setError] = useState<string>("");

  const [name, setName] = useState("");
  const [ip, setIp] = useState("");
  const [type, setType] = useState("");
  const [location, setLocation] = useState("");

  async function load() {
    setError("");
    try {
      const data = await listDevices();
      setDevices(Array.isArray(data) ? data : []);
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("Error al cargar dispositivos");
      }
      setDevices([]);
    }
  }

useEffect(() => {
  (async () => {
    await load();
  })();
}, []);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");

    try {
      await createDevice({
        name,
        ip_address: ip,
        device_type: type,
        location,
      });

      setName("");
      setIp("");
      setType("");
      setLocation("");

      await load();
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("Error al crear dispositivo");
      }
    }
  }

  async function remove(id: number) {
    setError("");
    try {
      await deleteDevice(id);
      await load();
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("Error al borrar dispositivo");
      }
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1>Network Device Inventory</h1>

      {error ? (
        <div style={{ background: "#fee2e2", padding: 12, marginBottom: 16 }}>
          {error}
        </div>
      ) : null}

      <h2>Agregar dispositivo</h2>
      <form onSubmit={submit} style={{ display: "grid", gap: 8, marginBottom: 24 }}>
        <input
          placeholder="Nombre"
          value={name}
          onChange={(ev) => setName(ev.target.value)}
        />
        <input
          placeholder="IP"
          value={ip}
          onChange={(ev) => setIp(ev.target.value)}
        />
        <input
          placeholder="Tipo (switch/router/ap...)"
          value={type}
          onChange={(ev) => setType(ev.target.value)}
        />
        <input
          placeholder="Ubicación"
          value={location}
          onChange={(ev) => setLocation(ev.target.value)}
        />
        <button type="submit">Crear</button>
      </form>

      <h2>Dispositivos</h2>

      <table width="100%" cellPadding={8} style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
            <th>ID</th>
            <th>Nombre</th>
            <th>IP</th>
            <th>Tipo</th>
            <th>Ubicación</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {devices.map((d) => (
            <tr key={d.id} style={{ borderBottom: "1px solid #eee" }}>
              <td>{d.id}</td>
              <td>{d.name}</td>
              <td>{d.ip_address}</td>
              <td>{d.device_type}</td>
              <td>{d.location}</td>
              <td>
                <button onClick={() => remove(d.id)}>Eliminar</button>
              </td>
            </tr>
          ))}

          {devices.length === 0 ? (
            <tr>
              <td colSpan={6} style={{ padding: 16 }}>
                No hay dispositivos.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}