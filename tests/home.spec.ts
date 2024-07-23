import { expect, test } from '@playwright/test';

test('home page has home elements', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('splash-logo')).toBeVisible();
  const startButton = await page.getByTestId('start-button');
  await expect(startButton).toBeVisible();
  await expect(startButton).toContainText('start posting time');
});

test('start button navigates to main nav', async ({ page }) => {
  await page.goto('/');
  const startButton = await page.getByTestId('start-button');
  await expect(startButton).toBeVisible();
  await startButton.click()
  const home = await page.getByTestId('home');
  await expect(home).toBeVisible();
  const new_client = await page.getByTestId('new_client');
  await expect (new_client).toBeVisible();

  const new_client_header = await page.getByTestId('new_client_header');
  // await expect (new_client_header).toBeVisible();

  const new_client_form = await page.getByTestId('new_client_form');
  await expect (new_client_header).toBeVisible();

  const new_client_name = await page.getByTestId('new_client_name');
  await expect (new_client_header).toBeVisible();

  const  new_client_name_input = await page.getByTestId(' new_client_name_input');
  await expect (new_client_header).toBeVisible();

  const  create_client_button = await page.getByTestId(' create_client_button');
  await expect (new_client_header).toBeVisible();
  await expect (new_client_header).toHaveValue('create')


});
