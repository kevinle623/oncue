import type { Invoice, PaymentMethod, Plan } from "@/types/api";
import { mockInvoices, mockPaymentMethod, mockPlan } from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function getPlan(): Promise<Plan> {
  await delay();
  return mockPlan;
}

export async function getPaymentMethod(): Promise<PaymentMethod | null> {
  await delay();
  return mockPaymentMethod;
}

export async function listInvoices(): Promise<Invoice[]> {
  await delay();
  return mockInvoices;
}
