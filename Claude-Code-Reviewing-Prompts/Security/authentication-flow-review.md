# Authentication Flow Review

# 认证流程审查

Conduct a comprehensive authentication security review:
进行全面的认证安全审查：

Check for:
检查以下内容：

1. Password hashing
   密码哈希

   * Uses `bcrypt.hash()` with salt rounds ≥ 10 (ideally 12); async, not sync; no double-hashing on updates.
     使用 `bcrypt.hash()`，盐轮次 ≥ 10（推荐 12）；使用异步而非同步；更新时不重复哈希。
   * `bcrypt.compare()` used for login.
     登录时使用 `bcrypt.compare()`。
2. JWT secret/key strength & storage
   JWT 密钥强度与存储

   * Secrets/keys not hardcoded; loaded from env or secret manager; separate keys for access vs refresh.
     密钥不硬编码；从环境变量或密钥管理器加载；访问令牌与刷新令牌使用独立密钥。
   * Strong entropy (≥256-bit for HS256) or asymmetric (RS256/ES256) with rotation plan.
     高熵值（HS256 ≥256 位）或非对称（RS256/ES256）并有轮换计划。
3. Token settings
   令牌设置

   * Access token TTL 5–15 minutes; refresh token TTL 7–30 days; sliding sessions bounded by a max session age.
     访问令牌 TTL 5–15 分钟；刷新令牌 TTL 7–30 天；滑动会话受最大会话时长约束。
   * JWT `algorithms`, `issuer (iss)`, `audience (aud)`, `subject (sub)`, `jti`, `iat`, `exp`, and optional `nbf` are enforced in `verify`.
     在 `verify` 中强制校验 JWT 的 `algorithms`、`iss`、`aud`、`sub`、`jti`、`iat`、`exp` 以及可选的 `nbf`。
4. Refresh token implementation
   刷新令牌实现

   * Rotation on every use and reuse detection (if old RT is presented, revoke the whole session family).
     每次使用时轮换，并检测重用（若旧刷新令牌被使用，撤销整个会话族）。
   * RTs stored in HttpOnly, Secure, SameSite cookie (not localStorage); hashed at rest if persisted; per-device tracking (`jti`, `ua`, `ip`, `expiresAt`).
     刷新令牌存储在 HttpOnly、Secure、SameSite Cookie 中（而非 localStorage）；持久化时哈希存储；按设备跟踪（`jti`、`ua`、`ip`、`expiresAt`）。
5. Session invalidation
   会话失效

   * On password change/reset, previously issued tokens are rejected (compare `pwdChangedAt` or increment `tokenVersion` vs `jwt.iat`).
     密码更改/重置后，拒绝之前颁发的令牌（比较 `pwdChangedAt` 或递增 `tokenVersion` 与 `jwt.iat` 对比）。
6. Brute force protection
   暴力破解防护

   * Rate limit login/reset/verify endpoints; progressive backoff per username+IP in a fast store (e.g., Redis); optional CAPTCHA after threshold.
     对登录/重置/验证端点实施速率限制；在快速存储（如 Redis）中按用户名+IP 实施渐进式退避；超过阈值后可选 CAPTCHA。
7. Account enumeration defenses
   账户枚举防御

   * Generic errors and identical status/timing for "user not found" vs "bad password"; optional jitter.
     对"用户不存在"和"密码错误"返回相同的通用错误和响应时间；可选加入随机抖动。
8. Password reset flow security
   密码重置流程安全

   * Reset tokens via `crypto.randomBytes(32)`, hashed at rest (SHA-256), short TTL (≤ 15–30 min), one-time use, invalidated after success.
     重置令牌使用 `crypto.randomBytes(32)` 生成，哈希存储（SHA-256），短 TTL（≤ 15–30 分钟），一次性使用，成功后立即失效。
   * No secrets in logs; throttle reset email sender.
     日志中不记录密钥；对重置邮件发送器进行节流。
9. Email verification
   邮箱验证

   * One-time, short-TTL verification tokens; server-side verified; no way to mark verified via mass-assignment/body fields.
     一次性、短 TTL 的验证令牌；服务器端验证；不能通过批量赋值/请求体字段标记为已验证。
10. SQL/NoSQL injection in auth paths
    认证路径中的 SQL/NoSQL 注入

    * No use of user-controlled operators in filters; query sanitization enabled; no `$where`; parameterized SQL if applicable.
      过滤器中不使用用户可控的操作符；启用查询净化；禁止 `$where`；适用时使用参数化 SQL。
11. AuthZ integrity
    授权完整性

    * Roles/permissions loaded server-side; deny-by-default; never trust role/claims purely from the JWT payload without verification and (for sensitive ops) a DB check.
      角色/权限在服务器端加载；默认拒绝；永远不要仅信任 JWT 载荷中的角色/声明，需经过验证，敏感操作还需数据库校验。
12. Cookie & CSRF configuration (if cookies used)
    Cookie 与 CSRF 配置（如使用 Cookie）

    * `HttpOnly`, `Secure`, `SameSite=Lax|Strict`, narrow `path`/`domain`, explicit `Max-Age`.
      设置 `HttpOnly`、`Secure`、`SameSite=Lax|Strict`，限制 `path`/`domain` 范围，显式设置 `Max-Age`。
    * CSRF protection on state-changing endpoints and refresh route (double-submit token or same-site strategy).
      对改变状态的端点和刷新路由实施 CSRF 防护（双提交令牌或同站策略）。
13. Input validation & normalization
    输入验证与规范化

    * Email/username normalization; length & charset checks; password policy; strong schema validation (zod/joi/celebrate).
      邮箱/用户名规范化；长度和字符集检查；密码策略；使用强模式验证（zod/joi/celebrate）。
14. Mass assignment risks
    批量赋值风险

    * Updates whitelist allowed fields; cannot set `role`, `emailVerified`, `passwordResetToken`, etc., from `req.body`.
      更新操作使用白名单字段；不能从 `req.body` 设置 `role`、`emailVerified`、`passwordResetToken` 等字段。
15. JWT misuse
    JWT 误用

    * No `jwt.decode()` for authorization decisions; always `jwt.verify()` with explicit `algorithms`.
      不使用 `jwt.decode()` 进行授权决策；始终使用 `jwt.verify()` 并显式指定 `algorithms`。
16. Logging & telemetry
    日志与遥测

    * No logging of passwords, tokens, reset links, or PII; structured logs with redaction/allowlist.
      不记录密码、令牌、重置链接或个人信息；使用带脱敏/白名单的结构化日志。
17. Dependency & crypto hygiene
    依赖与加密卫生

    * Maintained `jsonwebtoken` and `bcrypt` versions; no custom JWT parser; Node crypto used correctly; no MD5/SHA\* for password hashing.
      保持 `jsonwebtoken` 和 `bcrypt` 版本更新；不使用自定义 JWT 解析器；正确使用 Node crypto；不使用 MD5/SHA\* 进行密码哈希。
18. Transport & CORS
    传输与 CORS

    * HTTPS enforced; CORS locked to trusted origins; no wildcard credentials; preflight handled safely.
      强制使用 HTTPS；CORS 限定为受信来源；不使用通配符凭据；安全处理预检请求。
19. Open redirect / `next` param
    开放重定向 / `next` 参数

    * Post-login redirection restricted to vetted paths/origins; no arbitrary `next=` redirects.
      登录后重定向仅限于经过验证的路径/来源；不允许任意 `next=` 重定向。
20. Operational controls
    运营控制

    * Secret rotation procedure; key separation for environments; monitoring for suspicious auth patterns; alerting on RT reuse.
      密钥轮换流程；环境间密钥隔离；监控可疑认证模式；刷新令牌重用告警。

Provide:
输出要求：

* A structured finding report with the following for each issue:
  针对每个问题，提供结构化发现报告，包含：

  * Title, Severity (Critical/High/Medium/Low), CWE (if applicable), Evidence (file, function, line ranges), and a short Why it matters.
    标题、严重级别（严重/高/中/低）、CWE 编号（如适用）、证据（文件、函数、行范围），以及简短的危害说明。
  * Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).
    可利用性说明，以及在安全前提下的最小化 PoC 或复现步骤（不含真实密钥）。
  * Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.
    修复建议：精确的代码级修复或配置变更（欢迎提供代码片段），以及纵深防御指导。
* A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.
  综合风险评分（0–10），以及能最快降低风险的前 3–5 项优先修复项。
* A checklist diff: which items from the "Check for" list are Pass/Fail/Not Applicable.
  检查清单对比：标注"检查内容"列表中各项的通过/失败/不适用状态。

Constraints & style:
约束与风格：

* Be concrete and cite exact code locations and identifiers.
  具体引用精确的代码位置和标识符。
* Prefer minimal, drop-in fix snippets over prose.
  优先提供最简可直接替换的代码片段，而非长篇描述。
* Do not invent files or functions that aren't present; if context is missing, mark as Unable to verify and say what code would prove it.
  不要编造不存在的文件或函数；如缺少上下文，标记为"无法验证"并说明需要什么代码来证明。

Bonus (if applicable):
附加项（如适用）：

* Suggest hardening improvements (e.g., switching to RS256 with KMS-managed keys, adding `jti` blacklist service, adding device/session management UI, enabling `mongoose.set('sanitizeFilter', true)`).
  建议加固改进（如切换为 KMS 管理密钥的 RS256、添加 `jti` 黑名单服务、添加设备/会话管理 UI、启用 `mongoose.set('sanitizeFilter', true)`）。
* Provide quick tests to validate fixes (e.g., RT reuse test, password-changed invalidation test, NoSQLi payload test).
  提供快速测试以验证修复（如刷新令牌重用测试、密码更改失效测试、NoSQL 注入载荷测试）。

Provide specific vulnerabilities found with severity ratings.
列出发现的具体漏洞及其严重级别。

Write this into a markdown file and place it in the audits/ folder.
将结果写入 markdown 文件并放置在 audits/ 文件夹中。
