/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/predict',
        destination: 'https://voyage-imaging-backend.onrender.com/api/v1/predict',
      },
    ]
  },
}

module.exports = nextConfig
