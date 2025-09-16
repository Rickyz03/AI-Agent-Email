// TypeScript interfaces matching FastAPI schemas

export interface EmailIn {
  id?: string | number;
  thread_id?: string | number;
  subject: string;
  body: string;
  from_addr: string;
  to_addrs: string[];
  cc_addrs?: string[];
  bcc_addrs?: string[];
  language?: string;
}

export interface DraftOut {
  variants: string[];
  intent: string;
  priority: string;
  summary: string;
}

export interface PreferenceIn {
  tone_default: string;
  sign_off: string;
  signature_block: string;
}

export type PreferenceOut = PreferenceIn;
