"use client";
import { useState } from "react";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useAuth } from "@/store/auth";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { forgotPassword } = useAuth();

  const submit = async () => {
    if (!email) return;
    setError(null);
    setLoading(true);
    const result = await forgotPassword(email);
    setLoading(false);
    if (!result.ok) return setError(result.error);
    setSent(true);
  };

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">Reset your password</h1>
        {error && <div className="mt-4 px-3 py-2 rounded-[9px] bg-danger-bg border border-danger-border text-sm text-danger">{error}</div>}
        {sent ? (
          <div className="mt-5 px-4 py-3 rounded-[9px] bg-tint border border-tint-border text-sm text-accent">
            If an account exists for that email, a reset link is on its way.
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <Button className="w-full" onClick={submit} disabled={loading || !email}>
              {loading ? "Sending…" : "Send reset link"}
            </Button>
          </div>
        )}
      </Card>
    </div>
  );
}
