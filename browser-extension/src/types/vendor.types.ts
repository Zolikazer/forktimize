// Vendor strategy and configuration types for multi-vendor support

export interface VendorConfig {
  id: string;
  name: string;
  domain: string;
}

export interface CartResult {
  food: string;
  success: boolean;
  error?: string;
}

export interface AutoCartResponse {
  results: CartResult[];
  totalProcessed: number;
  successCount: number;
  failureCount: number;
}

export interface VendorValidationResult {
  isValid: boolean;
  message?: string;
}