"use client"

import { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Spinner } from "@/components/ui/spinner"

interface WeatherData {
  temperature: number
  humidity: number
  pressure: number
  weatherCode: number
  timestamp: string
}

interface ChartDataPoint {
  timestamp: string
  temperature: number
  humidity: number
  pressure: number
}

export default function Home() {
  const [currentData, setCurrentData] = useState<WeatherData | null>(null)
  const [chartData, setChartData] = useState<ChartDataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const response = await fetch("/api/weather")
        if (!response.ok) throw new Error("Failed to fetch weather data")
        const data = await response.json()
        setCurrentData(data.current)
        setChartData(data.history)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred")
      } finally {
        setLoading(false)
      }
    }

    fetchWeatherData()
    const interval = setInterval(fetchWeatherData, 5000)
    return () => clearInterval(interval)
  }, [])

  const getWeatherDescription = (code: number): string => {
    const descriptions: Record<number, string> = {
      0: "Clear sky",
      1: "Mainly clear",
      2: "Partly cloudy",
      3: "Overcast",
      45: "Foggy",
      48: "Depositing rime fog",
      51: "Light drizzle",
      53: "Moderate drizzle",
      55: "Dense drizzle",
      61: "Slight rain",
      63: "Moderate rain",
      65: "Heavy rain",
      71: "Slight snow",
      73: "Moderate snow",
      75: "Heavy snow",
      77: "Snow grains",
      80: "Slight rain showers",
      81: "Moderate rain showers",
      82: "Violent rain showers",
      85: "Slight snow showers",
      86: "Heavy snow showers",
      95: "Thunderstorm",
      96: "Thunderstorm with slight hail",
      99: "Thunderstorm with heavy hail",
    }
    return descriptions[code] || "Unknown"
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Kathmandu Environmental Monitor</h1>
          <p className="text-slate-400">Real-time environmental data with 5-second updates</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 rounded-lg bg-red-500/10 border border-red-500/30 p-4 text-red-400">{error}</div>
        )}

        {/* Current Data Cards */}
        {loading && !currentData ? (
          <div className="flex justify-center items-center h-64">
            <Spinner className="h-8 w-8" />
          </div>
        ) : currentData ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              {/* Temperature Card */}
              <Card className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 border-blue-400/30">
                <CardHeader className="pb-2">
                  <CardTitle className="text-blue-200 text-sm font-medium">Temperature</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-white">{currentData.temperature.toFixed(1)}°C</div>
                  <p className="text-blue-300 text-xs mt-2">{new Date(currentData.timestamp).toLocaleTimeString()}</p>
                </CardContent>
              </Card>

              {/* Humidity Card */}
              <Card className="bg-gradient-to-br from-cyan-500/20 to-cyan-600/20 border-cyan-400/30">
                <CardHeader className="pb-2">
                  <CardTitle className="text-cyan-200 text-sm font-medium">Humidity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-white">{currentData.humidity.toFixed(1)}%</div>
                  <p className="text-cyan-300 text-xs mt-2">Relative humidity</p>
                </CardContent>
              </Card>

              {/* Pressure Card */}
              <Card className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 border-purple-400/30">
                <CardHeader className="pb-2">
                  <CardTitle className="text-purple-200 text-sm font-medium">Pressure</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-white">{currentData.pressure.toFixed(1)}</div>
                  <p className="text-purple-300 text-xs mt-2">hPa</p>
                </CardContent>
              </Card>

              {/* Weather Condition Card */}
              <Card className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 border-orange-400/30">
                <CardHeader className="pb-2">
                  <CardTitle className="text-orange-200 text-sm font-medium">Condition</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm font-bold text-white leading-tight">
                    {getWeatherDescription(currentData.weatherCode)}
                  </div>
                  <p className="text-orange-300 text-xs mt-2">Code: {currentData.weatherCode}</p>
                </CardContent>
              </Card>
            </div>

            {/* Chart */}
            {chartData.length > 0 && (
              <Card className="bg-slate-800/50 border-slate-700/50">
                <CardHeader>
                  <CardTitle className="text-white">10-Minute Trend</CardTitle>
                  <CardDescription className="text-slate-400">Environmental parameters over time</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(100,116,139,0.2)" />
                      <XAxis dataKey="timestamp" stroke="rgb(148,163,184)" tick={{ fontSize: 12 }} />
                      <YAxis stroke="rgb(148,163,184)" tick={{ fontSize: 12 }} yAxisId="left" />
                      <YAxis stroke="rgb(168, 85, 247)" tick={{ fontSize: 12 }} yAxisId="right" orientation="right" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "rgba(15,23,42,0.8)",
                          border: "1px solid rgba(100,116,139,0.3)",
                          borderRadius: "8px",
                          color: "white",
                        }}
                      />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="temperature"
                        stroke="rgb(59, 130, 246)"
                        dot={false}
                        strokeWidth={2}
                        isAnimationActive={false}
                        yAxisId="left"
                      />
                      <Line
                        type="monotone"
                        dataKey="humidity"
                        stroke="rgb(34, 197, 94)"
                        dot={false}
                        strokeWidth={2}
                        isAnimationActive={false}
                        yAxisId="left"
                      />
                      <Line
                        type="monotone"
                        dataKey="pressure"
                        stroke="rgb(168, 85, 247)"
                        dot={false}
                        strokeWidth={2}
                        isAnimationActive={false}
                        yAxisId="right"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            )}
          </>
        ) : null}

        {/* Footer */}
        <div className="mt-8 text-center text-slate-500 text-sm">
          <p>Data updates every 5 seconds • Location: Kathmandu, Nepal (27.7172°N, 85.3240°E)</p>
        </div>
      </div>
    </main>
  )
}
