# Version Notes - Latest Package Versions (October 2025)

## Technology Stack Updates

This document tracks the latest stable versions of all dependencies used in the Nordic Thingy:52 MCP Server implementations.

Last updated: **October 18, 2025**

---

## Core MCP & TypeScript Packages

### @modelcontextprotocol/sdk
- **Version**: 1.20.1
- **Published**: 1 day ago (October 17, 2025)
- **Breaking Changes**: N/A (minor update)
- **Key Features**:
  - Latest MCP protocol implementation
  - Improved TypeScript support
  - Enhanced server/client capabilities
- **Installation**: `npm install @modelcontextprotocol/sdk@^1.20.1`

### TypeScript
- **Version**: 5.9.3
- **Released**: August 2025
- **Key Features**:
  - New `node20` module option alongside `nodenext`
  - Leaner `tsconfig.json` via `tsc --init`
  - Performance improvements (11% faster on large projects)
  - Cached instantiations on mappers
  - Optimized file existence checks
- **Installation**: `npm install typescript@^5.9.3`
- **Looking Ahead**: TypeScript 6.0 planned as transition to v7.0

---

## Validation & Schema Libraries

### Zod
- **Version**: 4.1.12
- **Released**: October 2025 (11 days ago)
- **Major Update**: Zod 4.0.0 released July 2025
- **Key Features**:
  - Significantly faster performance
  - Slimmer bundle size
  - More TypeScript compiler efficient
  - Long-requested features implemented
- **Breaking Changes**: Migration from v3 required
- **Popularity**: 37.8k GitHub stars, 31M weekly downloads
- **Installation**: `npm install zod@^4.1.12`
- **Migration Guide**: https://zod.dev/v4/versioning

---

## Logging & Utilities

### Winston
- **Version**: 3.18.3
- **Published**: 18 days ago (September 2025)
- **Status**: Stable, widely adopted (25,633 projects use it)
- **Key Features**:
  - Universal logging with multiple transports
  - Production-ready logging solution
  - OpenTelemetry instrumentation support
- **Installation**: `npm install winston@^3.18.3`

### dotenv
- **Version**: 16.4.5
- **Status**: Stable
- **Installation**: `npm install dotenv@^16.4.5`

---

## Testing Framework

### Vitest
- **Version**: 3.2.4 (stable)
- **Beta**: 4.0.0-beta.2 (June 24, 2025)
- **Major Releases**:
  - v3.0 released January 17, 2025
  - v3.2 released June 2, 2025
- **Key Features** (v3.2):
  - Improved Browser Mode
  - Enhanced TypeScript support
  - Better performance and developer experience
- **Installation**: `npm install vitest@^3.2.4`
- **Coverage**: `npm install @vitest/coverage-v8@^3.2.4`

---

## Bluetooth Low Energy (BLE) Libraries

### thingy52
- **Version**: 1.0.4
- **Status**: Specific to Nordic Thingy:52
- **Dependency**: Requires `noble-device`
- **Installation**: `npm install thingy52@^1.0.4`

### noble-device
- **Version**: 1.4.1
- **Published**: 9 years ago
- **Status**: Mature but not actively maintained
- **Purpose**: BLE peripheral abstraction
- **Used By**: thingy52 package
- **Installation**: `npm install noble-device@^1.4.1`

### @abandonware/noble (Recommended Alternative)
- **Version**: 1.9.2-26
- **Published**: 8 months ago
- **Status**: **Actively maintained** fork of original `noble`
- **Key Features**:
  - Cross-platform BLE central module
  - Better maintained than original `noble`
  - Compatible with modern Node.js versions
- **Installation**: `npm install @abandonware/noble@^1.9.2-26`
- **Use Case**: For new BLE implementations beyond thingy52

### @stoprocent/noble (Alternative)
- **Status**: Modern fork with Bluetooth 5.0 support
- **Use Case**: If you need bleeding-edge BLE features
- **Installation**: `npm install @stoprocent/noble`

---

## Development Tools

### TypeScript ESLint
- **Parser**: @typescript-eslint/parser@^8.20.0
- **Plugin**: @typescript-eslint/eslint-plugin@^8.20.0
- **ESLint**: ^9.18.0

### Prettier
- **Version**: 3.4.2
- **Status**: Latest code formatter

### tsx
- **Version**: 4.19.2
- **Purpose**: TypeScript execution for Node.js

### @types/node
- **Version**: 22.10.0
- **Purpose**: Node.js TypeScript definitions

---

## Python Implementation Versions

For comparison with the Python MCP server:

### Core Python Packages
- **mcp[cli]**: >=1.0.0
- **bleak**: >=0.21.0 (BLE library for Python)
- **pydantic**: >=2.0.0 (data validation)
- **pydantic-settings**: >=2.0.0

### Development Tools
- **pytest**: >=7.4.0
- **pytest-asyncio**: >=0.21.0
- **black**: >=23.7.0
- **ruff**: >=0.1.0
- **mypy**: >=1.5.0

---

## Version Compatibility Matrix

| Package | Node.js Required | TypeScript Required | Status |
|---------|-----------------|---------------------|--------|
| @modelcontextprotocol/sdk@1.20.1 | >=18.0.0 | >=5.0.0 | ✅ Production |
| TypeScript@5.9.3 | >=18.0.0 | N/A | ✅ Production |
| Zod@4.1.12 | >=18.0.0 | >=4.5.0 | ✅ Production |
| Vitest@3.2.4 | >=18.0.0 | >=5.0.0 | ✅ Production |
| Winston@3.18.3 | >=14.0.0 | Optional | ✅ Production |
| thingy52@1.0.4 | >=10.0.0 | Optional | ⚠️ Stable but old |
| @abandonware/noble@1.9.2-26 | >=12.0.0 | Optional | ✅ Active |

---

## Migration Notes

### Upgrading to Zod v4

```typescript
// Zod v3 (old)
import { z } from 'zod';
const schema = z.object({ name: z.string() });

// Zod v4 (new) - Same API, better performance
import { z } from 'zod';
const schema = z.object({ name: z.string() });
// No breaking changes in common use cases
```

### MCP SDK v1.20.1 Usage

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// Modern MCP server initialization
const server = new Server(
  {
    name: 'my-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);
```

### TypeScript 5.9 Module Resolution

```json
// tsconfig.json with TypeScript 5.9
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "node20",  // New in TS 5.9
    "moduleResolution": "node20",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

---

## Installation Commands

### Fresh Project Setup

```bash
# Initialize project
npm init -y

# Install production dependencies
npm install @modelcontextprotocol/sdk@^1.20.1 \
            thingy52@^1.0.4 \
            noble-device@^1.4.1 \
            @abandonware/noble@^1.9.2-26 \
            zod@^4.1.12 \
            winston@^3.18.3 \
            dotenv@^16.4.5

# Install development dependencies
npm install -D typescript@^5.9.3 \
               @types/node@^22.10.0 \
               @types/noble-device@^1.0.0 \
               tsx@^4.19.2 \
               vitest@^3.2.4 \
               @vitest/coverage-v8@^3.2.4 \
               eslint@^9.18.0 \
               @typescript-eslint/eslint-plugin@^8.20.0 \
               @typescript-eslint/parser@^8.20.0 \
               prettier@^3.4.2
```

### Updating Existing Project

```bash
# Update all dependencies to latest
npm update

# Or update specific packages
npm install @modelcontextprotocol/sdk@latest
npm install typescript@latest
npm install zod@latest
npm install vitest@latest
```

---

## Recommendations

### For New Projects (October 2025)

1. **Use TypeScript 5.9.3** - Latest stable with performance improvements
2. **Use Zod 4.1.12** - Significant performance gains over v3
3. **Use Vitest 3.2.4** - Stable with excellent TypeScript support
4. **Use @abandonware/noble** - Better maintained than original noble
5. **Use MCP SDK 1.20.1** - Latest protocol support

### For Production Deployments

- Lock versions in `package.json` (remove `^` prefix)
- Use `package-lock.json` for reproducible builds
- Test thoroughly after any major version updates
- Monitor for security updates via `npm audit`

### For Development

- Keep TypeScript and ESLint updated regularly
- Use `tsx` for fast TypeScript execution during development
- Enable strict type checking in `tsconfig.json`
- Use Vitest's watch mode for TDD

---

## Change Log Tracking

To stay updated on package changes:

- **MCP SDK**: https://github.com/modelcontextprotocol/typescript-sdk/releases
- **TypeScript**: https://devblogs.microsoft.com/typescript/
- **Zod**: https://github.com/colinhacks/zod/releases
- **Vitest**: https://github.com/vitest-dev/vitest/releases
- **Winston**: https://github.com/winstonjs/winston/releases

---

## Future Considerations

### TypeScript 6.0 (Expected 2026)
- Transition point for TypeScript 7.0
- Go-based compiler planned for v7.0
- Monitor announcements for migration planning

### Vitest 4.0 (Beta Available)
- Currently in beta (4.0.0-beta.2)
- Wait for stable release before production use
- Monitor release notes for breaking changes

### Node.js Compatibility
- Recommend Node.js 20 LTS (Active until 2026-04-30)
- Node.js 22 LTS (Active until 2027-04-30)
- Ensure all packages support your target Node.js version

---

Last updated: October 18, 2025
