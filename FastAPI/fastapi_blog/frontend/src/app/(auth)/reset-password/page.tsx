"use client";
import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { rules, check } from "@/lib/validation";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token");
  const expired = params.get("expired") === "1";
  const [pw, setPw] = useState(""), [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { resetPassword } = useAuth();
  const push = useToast((s) => s.push);

  const pErr = pw ? check(pw, rules.password) : null;
  const mismatch = confirm && pw !== confirm ? "Passwords don't match." : null;
  const valid = !pErr && !mismatch && pw && confirm && token;

  const submit = async () => {
    if (!valid || !token) return;
    setError(null);
    setLoading(true);
    const result = await resetPassword(token, pw);
    setLoading(false);
    if (!result.ok) {
      if (/expired|invalid/i.test(result.error)) return router.push("/reset-password?expired=1");
      return setError(result.error);
    }
    push("Password updated. Please log in.");
    router.push("/login");
  };

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">New password</h1>
        {expired || !token ? (
          <div className="mt-5 px-3 py-2 rounded-[9px] bg-danger-bg border border-danger-border text-sm text-danger">
            This reset link has expired. Request a new one.
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            {error && <div className="px-3 py-2 rounded-[9px] bg-danger-bg border border-danger-border text-sm text-danger">{error}</div>}
            <Input label="New password" type="password" value={pw} onChange={(e) => setPw(e.target.value)} error={pErr} />
            <Input label="Confirm password" type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} error={mismatch} />
            <Button className="w-full" onClick={submit} disabled={!valid || loading}>
              {loading ? "Updating…" : "Update password"}
            </Button>
          </div>
        )}
      </Card>
    </div>
  );
}
