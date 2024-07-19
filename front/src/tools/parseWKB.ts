const hexToBytes = (hex: string): Uint8Array => {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
    }
    return bytes;
}

const bytesToDouble = (bytes: Uint8Array, offset: number): number => {
    const buffer = bytes.buffer.slice(offset, offset + 8);
    const view = new DataView(buffer);
    return view.getFloat64(0, true);
}

const parseWKB = (wkb: string): { latitude: number, longitude: number } => {
    const bytes = hexToBytes(wkb);
    const longitude = bytesToDouble(bytes, 9);
    const latitude = bytesToDouble(bytes, 17);
    return { latitude, longitude };
}

export default parseWKB;
