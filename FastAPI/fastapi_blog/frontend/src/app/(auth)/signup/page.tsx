"use client";
import { useState } from "react";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { rules, check } from "@/lib/validation";

export default function SignupPage() {
  const [f, setF] = useState({ username: "", email: "", password: "" });
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement>) => setF({ ...f, [k]: e.target.value });

  const uErr = f.username ? check(f.username, rules.username) : null;
  const eErr = f.email ? check(f.email, rules.email) : null;
  const pErr = f.password ? check(f.password, rules.password) : null;
  const valid = !uErr && !eErr && !pErr && f.username && f.email && f.password;

  return (
    <div className="max-w-[420px] mx-auto py-8">
      <Card className="p-7">
        <h1 className="font-serif text-2xl font-bold text-ink">Create account</h1>
        <div className="mt-5 space-y-4">
          <Input label="Username" value={f.username} onChange={set("username")} error={uErr} valid={!!f.username && !uErr} hint="1–50 characters" />
          <Input label="Email" type="email" value={f.email} onChange={set("email")} error={eErr} valid={!!f.email && !eErr} />
          <Input label="Password" type="password" value={f.password} onChange={set("password")} error={pErr} hint="At least 5 characters" />
          <Button className="w-full" disabled={!valid}>Create account</Button>
        </div>
        <p className="mt-4 text-sm text-muted text-center">Already have one? <Link href="/login" className="text-accent">Log in</Link></p>
      </Card>
    </div>
  );
}