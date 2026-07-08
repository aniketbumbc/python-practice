
"use client";
import { useState } from "react";
import { useSearchParams } from "next/navigation";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { rules, check } from "@/lib/validation";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const expired = params.get("expired") === "1"; // token check happens server-side
  const [pw, setPw] = useState(""), [confirm, setConfirm] = useState("");
  const pErr = pw ? check(pw, rules.password) : null;
  const mismatch = confirm && pw !== confirm ? "Passwords don't match." : null;

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">New password</h1>
        {expired ? (
          <div className="mt-5 px-3 py-2 rounded-[9px] bg-danger-bg border border-danger-border text-sm text-danger">
            This reset link has expired. Request a new one.
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            <Input label="New password" type="password" value={pw} onChange={(e) => setPw(e.target.value)} error={pErr} />
            <Input label="Confirm password" type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} error={mismatch} />
            <Button className="w-full" disabled={!!pErr || !!mismatch || !pw}>Update password</Button>
          </div>
        )}
      </Card>
    </div>
  );
}