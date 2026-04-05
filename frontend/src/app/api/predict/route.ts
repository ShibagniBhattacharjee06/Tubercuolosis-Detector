import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!apiUrl) {
      return NextResponse.json(
        { error: "Backend URL (NEXT_PUBLIC_API_URL) is not configured." },
        { status: 500 }
      );
    }

    // Clean URL and prepare the backend call
    const cleanUrl = apiUrl.trim().replace(/\/$/, "") + "/api/v1/predict";

    // Forward the request to the Render backend (Server-to-Server)
    const response = await fetch(cleanUrl, {
      method: "POST",
      body: formData,
      // Increase timeout for free tier wake-up
      signal: AbortSignal.timeout(60000), 
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `Backend responded with ${response.status}: ${errorText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error: any) {
    console.error("Proxy Error:", error);
    return NextResponse.json(
      { error: "Proxy failed to connect to backend: " + error.message },
      { status: 500 }
    );
  }
}
