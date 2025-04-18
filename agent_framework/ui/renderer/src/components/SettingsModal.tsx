import { useState, useEffect } from "react";
import { ipcRenderer } from "electron";
import { config, saveConfig, getEndpoint } from "../lib/config";

export default function SettingsModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [backendCfg, setBackendCfg] = useState<any>({});
  const [frontendCfg, setFrontendCfg] = useState<any>({ ...config });
  
  useEffect(() => {
    if (open) {
      ipcRenderer.invoke("get-config").then(setBackendCfg);
      setFrontendCfg({ ...config });
    }
  }, [open]);
  
  const save = () => {
    // Save backend config
    ipcRenderer.invoke("set-config", backendCfg);
    
    const oauthEndpoint = getEndpoint("oauthService");
    fetch(`${oauthEndpoint}/config`, { 
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify(backendCfg) 
    });
    
    // Save frontend config
    saveConfig(frontendCfg);
    
    onClose();
  };
  
  return (
    open && (
      <div className="fixed inset-0 bg-black/60 flex items-center justify-center">
        <div className="bg-white rounded p-6 space-y-4 w-[500px] max-h-[90vh] overflow-y-auto">
          <h2 className="font-semibold">Backend Settings</h2>
          {[
            ["chat", "model"],
            ["chat", "api_key"],
            ["chat", "base_url"],
            ["embed", "model"],
            ["embed", "api_key"],
            ["embed", "base_url"],
            ["endpoints", "oauth_service"],
            ["endpoints", "task_executor"],
            ["endpoints", "mcp_servers_base"]
          ].map(([sect, key]) => (
            <div key={`${sect}.${key}`} className="flex items-center">
              <label className="w-32 font-medium text-sm">{sect}.{key}</label>
              <input
                className="flex-1 border p-1 text-sm"
                placeholder={`${sect}.${key}`}
                value={backendCfg?.[sect]?.[key] || ""}
                onChange={(e) => setBackendCfg({ 
                  ...backendCfg, 
                  [sect]: { ...(backendCfg[sect] || {}), [key]: e.target.value } 
                })}
              />
            </div>
          ))}
          
          <h2 className="font-semibold pt-4">Frontend Endpoints</h2>
          {Object.keys(frontendCfg.endpoints || {}).map((key) => (
            <div key={key} className="flex items-center">
              <label className="w-32 font-medium text-sm">endpoints.{key}</label>
              <input
                className="flex-1 border p-1 text-sm"
                placeholder={`endpoint.${key}`}
                value={frontendCfg.endpoints[key] || ""}
                onChange={(e) => setFrontendCfg({ 
                  ...frontendCfg, 
                  endpoints: { ...frontendCfg.endpoints, [key]: e.target.value } 
                })}
              />
            </div>
          ))}
          
          <div className="pt-2">
            <button onClick={save} className="bg-blue-500 text-white px-3 py-1 rounded">Save</button>
          </div>
        </div>
      </div>
    )
  );
} 