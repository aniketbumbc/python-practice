"use client";
import { useState } from "react";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">Reset your password</h1>
        {sent ? (
          <div className="mt-5 px-4 py-3 rounded-[9px] bg-tint border border-tint-border text-sm text-accent">
            If an account exists for that email, a reset link is on its way.
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <Button className="w-full" onClick={() => setSent(true)}>Send reset link</Button>
          </div>
        )}
      </Card>
    </div>
  );
}