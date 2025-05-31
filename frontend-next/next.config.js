/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // API重写，代理到后端服务
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3000'}/api/:path*`,
      },
    ];
  },

  // 环境变量
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3000',
  },

  // 图片配置
  images: {
    domains: ['localhost'],
  },

  // 实验性功能
  experimental: {
    appDir: true,
  },
};

module.exports = nextConfig; 