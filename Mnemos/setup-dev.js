#!/usr/bin/env node

const fs = require('fs')
const path = require('path')

console.log('🚀 Setting up Mnemos development environment...\n')

// Create .env.local if it doesn't exist
const envPath = path.join(__dirname, '.env.local')
const envExamplePath = path.join(__dirname, '.env.example')

if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
  fs.copyFileSync(envExamplePath, envPath)
  console.log('✅ Created .env.local from .env.example')
} else {
  console.log('ℹ️  .env.local already exists or .env.example not found')
}

// Check if required directories exist
const requiredDirs = [
  'src/components',
  'src/views', 
  'src/hooks',
  'src/utils',
  'src/assets',
  'src/test'
]

requiredDirs.forEach(dir => {
  const fullPath = path.join(__dirname, dir)
  if (fs.existsSync(fullPath)) {
    console.log(`✅ Directory exists: ${dir}`)
  } else {
    console.log(`❌ Directory missing: ${dir}`)
  }
})

console.log('\n🎉 Setup complete! Run "npm install" then "npm run dev" to start developing.')
console.log('\nUseful commands:')
console.log('  npm run dev          - Start development server')
console.log('  npm run build        - Build for production')  
console.log('  npm run test         - Run tests')
console.log('  npm run lint         - Run linter')
console.log('  npm run mobile:build - Build for mobile')