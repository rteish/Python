import { NextResponse } from "next/server"

interface OpenMeteoResponse {
  latitude: number
  longitude: number
  current: {
    temperature_2m: number
    relative_humidity_2m: number
    pressure_msl: number
    weather_code: number
    time: string
  }
  hourly: {
    time: string[]
    temperature_2m: number[]
    relative_humidity_2m: number[]
    pressure_msl: number[]
  }
}

// Store historical data in memory (for simplicity)
const historyBuffer: Array<{
  timestamp: string
  temperature: number
  humidity: number
  pressure: number
}> = []

async function fetchOpenMeteoData() {
  try {
    const response = await fetch(
      "https://api.open-meteo.com/v1/forecast?" +
        "latitude=27.7172&longitude=85.3240&" +
        "current=temperature_2m,relative_humidity_2m,pressure_msl,weather_code&" +
        "hourly=temperature_2m,relative_humidity_2m,pressure_msl&" +
        "timezone=Asia/Kathmandu",
    )

    if (!response.ok) {
      throw new Error(`Open-Meteo API error: ${response.status}`)
    }

    const data: OpenMeteoResponse = await response.json()
    return data
  } catch (error) {
    console.error("Error fetching Open-Meteo data:", error)
    throw error
  }
}

export async function GET() {
  try {
    const data = await fetchOpenMeteoData()

    const currentData = {
      temperature: data.current.temperature_2m,
      humidity: data.current.relative_humidity_2m,
      pressure: data.current.pressure_msl,
      weatherCode: data.current.weather_code,
      timestamp: data.current.time,
    }

    const now = new Date()
    const timeString = now.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    })

    historyBuffer.push({
      timestamp: timeString,
      temperature: currentData.temperature,
      humidity: currentData.humidity,
      pressure: currentData.pressure,
    })

    if (historyBuffer.length > 120) {
      historyBuffer.shift()
    }

    return NextResponse.json({
      current: currentData,
      history: historyBuffer,
      location: {
        latitude: data.latitude,
        longitude: data.longitude,
        name: "Kathmandu, Nepal",
      },
    })
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json({ error: "Failed to fetch weather data" }, { status: 500 })
  }
}
