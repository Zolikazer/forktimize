#!/usr/bin/env node

// Script to remove development URLs from manifests for production
const fs = require('fs');
const path = require('path');

function stripDevUrls(inputFile, outputFile) {
    console.log(`🔧 Stripping dev URLs: ${inputFile} -> ${outputFile}`);
    
    const manifest = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const prodManifest = { ...manifest };
    
    // Development URL patterns to remove
    const devUrlPatterns = [
        'http://localhost',
        'http://127.0.0.1',
        'localhost'
    ];
    
    function isDevUrl(url) {
        return devUrlPatterns.some(pattern => url.includes(pattern));
    }
    
    // Handle permissions (Firefox MV2)
    if (prodManifest.permissions) {
        prodManifest.permissions = prodManifest.permissions.filter(perm => !isDevUrl(perm));
    }
    
    // Handle host_permissions (Chrome MV3)
    if (prodManifest.host_permissions) {
        prodManifest.host_permissions = prodManifest.host_permissions.filter(perm => !isDevUrl(perm));
    }
    
    // Handle content_scripts
    if (prodManifest.content_scripts) {
        prodManifest.content_scripts = prodManifest.content_scripts.map(script => ({
            ...script,
            matches: script.matches.filter(match => !isDevUrl(match))
        })).filter(script => script.matches.length > 0);
    }
    
    // Write production manifest
    fs.writeFileSync(outputFile, JSON.stringify(prodManifest, null, 2));
    console.log(`✅ Created ${outputFile} (dev URLs removed)`);
}

function main() {
    const baseDir = path.join(__dirname, '..');
    
    try {
        stripDevUrls(
            path.join(baseDir, 'manifest-chrome.json'),
            path.join(baseDir, 'manifest-chrome-prod.json')
        );
        
        stripDevUrls(
            path.join(baseDir, 'manifest-firefox.json'),
            path.join(baseDir, 'manifest-firefox-prod.json')
        );
        
        console.log('\n🎉 Production manifests ready for store submission!');
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { stripDevUrls };