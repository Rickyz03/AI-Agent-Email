export interface EmailIn {
  id?: string;
  thread_id?: string;
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
