import { Buffer } from 'buffer';

const createWKB = (lon: number, lat: number, srid: number = 4326): string => {
    const buffer = Buffer.alloc(25);

    buffer.writeUInt8(1, 0);
    buffer.writeUInt32LE(1, 1);
    buffer.writeUInt32LE(srid, 5);
    buffer.writeDoubleLE(lon, 9);
    buffer.writeDoubleLE(lat, 17);
    return buffer.toString('hex').toUpperCase();
}

export default createWKB;