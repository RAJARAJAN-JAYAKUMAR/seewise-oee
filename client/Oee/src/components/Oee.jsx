import React, { useState, useEffect } from "react";
import axios from "axios";

function Oee() {
  const [machines, setMachines] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/oee/")
      .then((response) => {
        setMachines(response.data);
      })
      .catch((error) => {
        setError(error.message);
      });
  }, []);

  return (
    <div className="border border-b-2 h-80 p-4 bg-blue-300 ">
      <h1 className="text-xl font-bold mb-4">Machine OEE Data</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="overflow-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr className="bg-gray-200 text-left">
              <th className="px-4 py-2 border-b border-gray-300">
                Machine Name
              </th>
              <th className="px-4 py-2 border-b border-gray-300">
                Serial Number
              </th>
              <th className="px-4 py-2 border-b border-gray-300">
                Availability
              </th>
              <th className="px-4 py-2 border-b border-gray-300">
                Performance
              </th>
              <th className="px-4 py-2 border-b border-gray-300">Quality</th>
              <th className="px-4 py-2 border-b border-gray-300">OEE</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((machine, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.machine.machine_name}
                </td>
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.machine.machine_serial_no}
                </td>
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.oee_data.availability.toFixed(2)}%
                </td>
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.oee_data.performance.toFixed(2)}%
                </td>
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.oee_data.quality.toFixed(2)}%
                </td>
                <td className="px-4 py-2 border-b border-gray-200">
                  {machine.oee_data.oee.toFixed(2)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Oee;
