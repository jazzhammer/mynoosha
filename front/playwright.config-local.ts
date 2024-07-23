import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
	workers: 5,
	retries: 1,
	webServer: {
		command: 'npm run build && npm run preview',
		port: 4173
	},
	use: {
		baseURL: 'http://localhost:8002',
		screenshot: 'only-on-failure',
		video: 'retain-on-failure',
		trace: 'retain-on-failure',
	},
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	projects: [
		{
			name: 'chromium',
			use: { browserName: 'chromium' }
		},
		{
			name: 'firefox',
			use: { browserName: 'firefox' }
		},
		{
			name: 'webKit',
			use: { browserName: 'webkit' }
		}
	]
};
export default config;
