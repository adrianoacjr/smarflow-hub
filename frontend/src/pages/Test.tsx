import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function TestPage() {
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const backendUrl = import.meta.env.VITE_API_BASE_URL;

    const testBackend = async () => {
        setLoading(true);
        try {
            const res = await fetch(`${backendUrl}/health`);
            console.log(res);
            const data = await res.json();
            setResult(data);
        } catch (error) {
            setResult({ error: "Failed to fetch /health" });
        }
        setLoading(false);
    };

    return (
        <div className="flex justify-center p-8">
            <Card className="w-[500px]">
                <CardHeader>
                    <CardTitle>Test Backend Connection</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="mb-4 text-sm text-muted-foreground">
                        Backend URL: <strong>{backendUrl}</strong>
                    </p>

                    <Button onClick={testBackend} disabled={loading}>
                        {loading ? "Testing..." : "Test /health"}
                    </Button>

                    <pre className="mt-4 p-3 bg-muted rounded text-sm">
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </CardContent>
            </Card>
        </div>
    );
}
