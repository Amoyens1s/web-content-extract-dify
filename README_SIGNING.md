# Dify 插件签名指南

为了确保插件的安全性，Dify 现在要求插件必须经过数字签名才能安装。本指南将说明如何为您的插件设置签名。

## 重要安全说明

**私钥安全**：私钥文件（`.private.pem`）**绝不能**包含在代码仓库中或公开分享。这些文件应该：
- 保存在安全的本地位置
- 添加到 `.gitignore` 文件中以防止意外提交
- 仅在需要签名时使用

## 生成密钥对

项目提供了一个便捷的脚本来生成密钥对：

```bash
# 运行项目提供的脚本
./scripts/generate-keys.sh
```

或者，您也可以直接使用 Dify CLI 命令：

```bash
dify signature generate --filename my-plugin-key
```

这将生成两个文件：
- `my-plugin-key.private.pem` - 私钥（必须保密，不要提交到仓库）
- `my-plugin-key.public.pem` - 公钥（可以公开）

## GitHub Actions 签名配置

为了在 GitHub Actions 中自动签名插件，您需要将私钥添加到仓库的 Secrets 中：

1. 进入您的 GitHub 仓库
2. 点击 "Settings" 选项卡
3. 在左侧菜单中点击 "Secrets and variables" → "Actions"
4. 点击 "New repository secret" 按钮
5. 添加以下 secret：

   - Name: `PLUGIN_PRIVATE_KEY`
     Value: (粘贴您的私钥内容，包括 `-----BEGIN PRIVATE KEY-----` 和 `-----END PRIVATE KEY-----`)

注意：公钥不需要作为 secret 存储，因为它可以公开。

## 手动签名插件

如果您想手动签名插件，可以使用以下命令：

```bash
# 为插件包签名
dify signature sign your-plugin.difypkg --private_key my-plugin-key.private.pem

# 验证签名
dify signature verify your-plugin.signed.difypkg --public_key my-plugin-key.public.pem
```

## 密钥安全注意事项

- **永远不要**将私钥提交到代码仓库中
- 将私钥文件添加到 `.gitignore` 文件中
- 公钥可以安全地包含在仓库中或与插件一起分发
- 定期轮换您的密钥对以提高安全性
- 如果您怀疑密钥已被泄露，请立即生成新的密钥对并更新您的 secrets

## 插件安装

签名后的插件文件将以 `.signed.difypkg` 扩展名结尾。这个文件可以安全地安装到启用了插件验证的 Dify 实例中。

## 开源项目最佳实践

对于开源项目：
1. 不要在仓库中包含任何 `.pem` 文件
2. 在 `.gitignore` 中添加 `*.pem` 来防止意外提交
3. 为贡献者提供清晰的签名指南
4. 考虑使用 GitHub Actions 自动签名发布版本
5. 在文档中明确说明私钥的安全要求