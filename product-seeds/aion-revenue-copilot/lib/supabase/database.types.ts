export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export type Database = {
  public: {
    Tables: {
      organizations: {
        Row: {
          id: string;
          name: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["organizations"]["Insert"]>;
      };
      organization_members: {
        Row: {
          id: string;
          organization_id: string;
          user_id: string;
          role: "owner" | "admin" | "rep";
          created_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          user_id: string;
          role?: "owner" | "admin" | "rep";
          created_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["organization_members"]["Insert"]>;
      };
      business_contexts: {
        Row: {
          id: string;
          organization_id: string;
          industry: string;
          services: Json;
          likely_pains: Json;
          relevant_offer: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          industry: string;
          services?: Json;
          likely_pains?: Json;
          relevant_offer?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["business_contexts"]["Insert"]>;
      };
      leads: {
        Row: {
          id: string;
          organization_id: string;
          business_context_id: string | null;
          company_name: string;
          contact_name: string | null;
          source: string | null;
          status: "new" | "contacted" | "qualified" | "closed";
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          business_context_id?: string | null;
          company_name: string;
          contact_name?: string | null;
          source?: string | null;
          status?: "new" | "contacted" | "qualified" | "closed";
          created_at?: string;
          updated_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["leads"]["Insert"]>;
      };
      calls: {
        Row: {
          id: string;
          lead_id: string;
          rep_user_id: string;
          phase: "pre" | "active" | "post" | "completed";
          started_at: string;
          ended_at: string | null;
        };
        Insert: {
          id?: string;
          lead_id: string;
          rep_user_id: string;
          phase?: "pre" | "active" | "post" | "completed";
          started_at?: string;
          ended_at?: string | null;
        };
        Update: Partial<Database["public"]["Tables"]["calls"]["Insert"]>;
      };
      call_outcomes: {
        Row: {
          id: string;
          call_id: string;
          qualification: "unqualified" | "exploring" | "qualified" | "disqualified";
          pain_points: Json;
          objections: Json;
          next_action: string;
          transcript_summary: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          call_id: string;
          qualification: "unqualified" | "exploring" | "qualified" | "disqualified";
          pain_points?: Json;
          objections?: Json;
          next_action: string;
          transcript_summary?: string | null;
          created_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["call_outcomes"]["Insert"]>;
      };
      event_log: {
        Row: {
          id: string;
          organization_id: string;
          call_id: string | null;
          lead_id: string | null;
          event_type: "crm" | "learning";
          payload: Json;
          external_id: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          call_id?: string | null;
          lead_id?: string | null;
          event_type: "crm" | "learning";
          payload?: Json;
          external_id?: string | null;
          created_at?: string;
        };
        Update: Partial<Database["public"]["Tables"]["event_log"]["Insert"]>;
      };
    };
  };
};

export type LeadRow = Database["public"]["Tables"]["leads"]["Row"];
export type BusinessContextRow = Database["public"]["Tables"]["business_contexts"]["Row"];
export type CallOutcomeRow = Database["public"]["Tables"]["call_outcomes"]["Row"];
