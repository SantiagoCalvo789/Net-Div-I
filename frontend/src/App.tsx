import { useEffect, useState } from "react";
import { createDevice, deleteDevice, listDevices } from "./api";
import type { Device } from "./api";

import "./App.css";

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
    <div className="page">
      <div className="container">
        <header className="header">
          <h1 className="title">Network Device Inventory</h1>
          <p className="subtitle">Frontend (React) conectado a FastAPI + PostgreSQL</p>
        </header>

        {error ? <div className="alert">{error}</div> : null}

        <section className="card">
          <h2 className="cardTitle">Agregar dispositivo</h2>

          <form onSubmit={submit} className="form">
            <div className="grid">
              <label className="field">
                <span className="label">Nombre</span>
                <input
                  className="input"
                  placeholder="Switch-Core-01"
                  value={name}
                  onChange={(ev) => setName(ev.target.value)}
                />
              </label>

              <label className="field">
                <span className="label">IP</span>
                <input
                  className="input"
                  placeholder="192.168.1.10"
                  value={ip}
                  onChange={(ev) => setIp(ev.target.value)}
                />
              </label>

              <label className="field">
                <span className="label">Tipo</span>
                <input
                  className="input"
                  placeholder="switch/router/access-point/firewall..."
                  value={type}
                  onChange={(ev) => setType(ev.target.value)}
                />
              </label>

              <label className="field">
                <span className="label">Ubicación</span>
                <input
                  className="input"
                  placeholder="Data Center - Rack A1"
                  value={location}
                  onChange={(ev) => setLocation(ev.target.value)}
                />
              </label>
            </div>

            <div className="actions">
              <button className="button" type="submit">
                Crear
              </button>
            </div>
          </form>
        </section>

        <section className="card">
          <div className="cardHeader">
            <h2 className="cardTitle">Dispositivos</h2>
            <button className="button secondary" type="button" onClick={load}>
              Refrescar
            </button>
          </div>

          <div className="tableWrap">
            <table className="table">
              <thead>
                <tr>
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
                  <tr key={d.id}>
                    <td>{d.id}</td>
                    <td>{d.name}</td>
                    <td>{d.ip_address}</td>
                    <td>{d.device_type}</td>
                    <td>{d.location}</td>
                    <td className="tdRight">
                      <button className="button danger" type="button" onClick={() => remove(d.id)}>
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}

                {devices.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="empty">
                      No hay dispositivos.
                    </td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}