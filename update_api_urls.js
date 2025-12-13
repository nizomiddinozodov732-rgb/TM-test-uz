/**
 * Helper script to update API URLs in HTML files for Vercel deployment
 * 
 * This script updates all HTML files to use environment-aware API URLs:
 * - Local development: http://localhost:5000/api
 * - Production (Vercel): /api (relative URL)
 * 
 * Usage:
 * 1. Run this script: node update_api_urls.js
 * 2. Or manually update each HTML file with the code below
 */

const fs = require('fs');
const path = require('path');

const htmlFiles = [
  'Index.html',
  'kirish.html',
  'test_tanlov.html',
  'test_yuklash.html',
  'results.html',
  'ishlash.html'
];

// The new API URL code that auto-detects environment
const newApiUrlCode = `        // API URL - auto-detects environment (local vs Vercel)
        const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://localhost:5000/api'
            : window.location.origin + '/api';`;

// Pattern to find and replace
const oldApiUrlPattern = /const API_URL = ['"]http:\/\/localhost:5000\/api['"];?/g;

htmlFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Replace the old API_URL line
        if (oldApiUrlPattern.test(content)) {
            content = content.replace(oldApiUrlPattern, newApiUrlCode);
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Updated ${file}`);
        } else {
            console.log(`⚠️  ${file} - API_URL pattern not found or already updated`);
        }
    } else {
        console.log(`❌ ${file} - File not found`);
    }
});

console.log('\n✨ Done! All HTML files updated with environment-aware API URLs.');

