"use client";

import { useQuery } from "@tanstack/react-query";
import { getPaymentMethod, getPlan, listInvoices } from "@/lib/api/billing";
import { queryKeys } from "@/lib/query-keys";

export function usePlan() {
  return useQuery({
    queryKey: queryKeys.plan,
    queryFn: getPlan,
  });
}

export function usePaymentMethod() {
  return useQuery({
    queryKey: queryKeys.paymentMethod,
    queryFn: getPaymentMethod,
  });
}

export function useInvoices() {
  return useQuery({
    queryKey: queryKeys.invoices,
    queryFn: listInvoices,
  });
}
