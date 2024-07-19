import Bridge from "../models/bridge";
import parseWKB from "./parseWKB";

const fetchBridges = async (): Promise<Bridge[]> => {
    try {
        const response = await fetch('http://127.0.0.1:8000/bridges/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data: any[] = await response.json();
        const processedData: Bridge[] = data.map((bridge: any) => {
            const { latitude, longitude } = parseWKB(bridge.location);
            return { ...bridge, latitude: latitude, longitude: longitude };
        });
        return processedData;
    } catch (error) {
        return [];
    }
};

export default fetchBridges;
