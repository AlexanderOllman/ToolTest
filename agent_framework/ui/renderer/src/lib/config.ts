/**
 * Application configuration
 * This file provides endpoints and configuration for the frontend
 */

// Default configuration
export const defaultConfig = {
  endpoints: {
    socketIO: "http://localhost:8001",
    oauthService: "http://localhost:9300",
    taskExecutor: "http://localhost:8001"
  }
};

// Try to load config from localStorage or use defaults
const loadConfig = () => {
  if (typeof window === 'undefined') return defaultConfig;
  
  try {
    const stored = localStorage.getItem('app_config');
    return stored ? { ...defaultConfig, ...JSON.parse(stored) } : defaultConfig;
  } catch (e) {
    console.error('Error loading config from localStorage', e);
    return defaultConfig;
  }
};

// Current config
export const config = loadConfig();

// Save config to localStorage
export const saveConfig = (newConfig: typeof config) => {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem('app_config', JSON.stringify(newConfig));
    Object.assign(config, newConfig);
  } catch (e) {
    console.error('Error saving config to localStorage', e);
  }
};

// Get a specific endpoint
export const getEndpoint = (name: keyof typeof config.endpoints) => {
  return config.endpoints[name];
}; 