function decodeUplink(input) {
  const bytes = input.bytes;

  if (bytes.length !== 26) {
    return {
      errors: ["Payload length mismatch. Expected 26 bytes."]
    };
  }
  return {
    data: {
      temperatura: roundTo2Decimals(bytesToFloat(bytes, 0)),
      humedad: roundTo2Decimals(bytesToFloat(bytes, 4)),
      accel_x: roundTo2Decimals(bytesToFloat(bytes, 8)),
      accel_y: roundTo2Decimals(bytesToFloat(bytes, 12)),
      accel_z: roundTo2Decimals(bytesToFloat(bytes, 16)),
      climaPercentage: roundTo2Decimals(bytesToFloat(bytes, 20)),
      airQuality: decodeAirQuality(String.fromCharCode(bytes[24])),
      clima: decodeClima(String.fromCharCode(bytes[25]))
    }
  };
}

function roundTo2Decimals(value) {
  return Math.round(value * 100) / 100;
}


function bytesToFloat(bytes, index) {
  const buffer = new ArrayBuffer(4);
  const view = new DataView(buffer);
  for (let i = 0; i < 4; i++) {
    view.setUint8(i, bytes[index + i]);
  }
  return view.getFloat32(0, false); // false = big-endian
}

function decodeAirQuality(input){
  const dataMap = {
    "S": "Excelente",
    "A": "Buena",
    "B": "Moderada",
    "F": "Mala"
  }
  return dataMap[input]
}

function decodeClima(input){
  const dataMap = {
        "N": "Nublado",
        "B": "Brumoso",
        "L": "Lluvioso",
        "S": "Soleado",
        "A": "Amanecer",
    }
  return dataMap[input]
}