// E2E Puppeteer test for Car Fleet Manager (Reflex frontend + Django backend)
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  page.setDefaultTimeout(10000);

  // 1. Visit login page
  await page.goto('http://localhost:3001/login');
  await page.waitForSelector('input[aria-label="Username"]');
  await page.type('input[aria-label="Username"]', 'admin'); // adjust username as needed
  await page.type('input[aria-label="Password"]', 'password123'); // adjust password as needed
  await page.click('button[type="submit"]');

  // 2. Wait for dashboard (redirect)
  await page.waitForSelector('h2'); // Dashboard heading
  const heading = await page.$eval('h2', el => el.textContent);
  if (!heading.includes('Fleet Dashboard')) throw new Error('Login failed or dashboard not loaded');

  // 3. Navigate to Vehicles page
  await page.click('a[href="/vehicles"]');
  await page.waitForSelector('th'); // Table header
  const vehicleTableExists = await page.$$eval('th', ths => ths.some(th => th.textContent.includes('Brand')));
  if (!vehicleTableExists) throw new Error('Vehicles table not found');

  // 4. Add a vehicle
  await page.click('button[aria-label="Add vehicle"]');
  await page.waitForSelector('input[aria-label="Brand"]');
  await page.type('input[aria-label="Brand"]', 'TestBrand');
  await page.type('input[aria-label="Model"]', 'TestModel');
  await page.type('input[aria-label="Year"]', '2025');
  await page.type('input[aria-label="License Plate"]', 'TEST-123');
  await page.type('input[aria-label="VIN"]', 'VIN1234567890');
  await page.type('input[aria-label="Status"]', 'AVAILABLE');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(1000);
  // Confirm vehicle appears in table
  const vehicleRow = await page.$$eval('tr', rows => rows.some(row => row.textContent.includes('TestBrand')));
  if (!vehicleRow) throw new Error('Vehicle not added');

  // 5. Navigate to Drivers page
  await page.click('a[href="/drivers"]');
  await page.waitForSelector('th');
  // Add similar driver test if needed

  // 6. Logout (if implemented)
  // await page.click('button[aria-label="Logout"]');

  await browser.close();
  console.log('E2E test completed successfully.');
})();
