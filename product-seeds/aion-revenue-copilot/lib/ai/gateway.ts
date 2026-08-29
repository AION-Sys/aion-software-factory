export type AiGatewayRequest = {
  model?: string;
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
};

export type AiGatewayResponse = {
  content: string;
};

/**
 * Client for AION AI Gateway. V1 stub; Builder implements HTTP client.
 */
export async function complete(_request: AiGatewayRequest): Promise<AiGatewayResponse> {
  return {
    content: "AI Gateway not configured — wire AION_AI_GATEWAY_URL in deployment.",
  };
}
