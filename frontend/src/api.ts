export type Device = {
  id: number;
  name: string;
  ip_address: string;
  device_type: string;
  location: string;
};

export type DeviceCreate = {
  name: string;
  ip_address: string;
  device_type: string;
  location: string;
};

const API_BASE = "http://127.0.0.1:8000";

export async function listDevices(): Promise<Device[]> {
  const res = await fetch(`${API_BASE}/devices`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function createDevice(payload: DeviceCreate): Promise<Device> {
  const res = await fetch(`${API_BASE}/devices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (res.status === 409) {
    throw new Error("IP duplicada");
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

  return res.json();
}

export async function deleteDevice(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/devices/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error(`Error ${res.status}`);
}