#!/usr/bin/env node

import fetch from 'node-fetch';

// Test the Open-Meteo API directly
async function testWeatherAPI() {
  console.log('Testing Open-Meteo API connection...\n');
  
  const latitude = 52.52;  // Berlin
  const longitude = 13.41;
  
  try {
    // Test current weather
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code`;
    
    console.log('Fetching current weather for Berlin...');
    const response = await fetch(url);
    const data = await response.json();
    
    console.log('✓ API connection successful!\n');
    console.log('Current weather data:');
    console.log(JSON.stringify(data.current, null, 2));
    console.log('\nLocation:', data.latitude, ',', data.longitude);
    console.log('Timezone:', data.timezone);
    
  } catch (error) {
    console.error('✗ API connection failed:', error.message);
  }
}

testWeatherAPI();
