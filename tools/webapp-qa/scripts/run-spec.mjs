import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

import puppeteer from "puppeteer";

function parseArgs(argv) {
  const args = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (!token.startsWith("--")) {
      continue;
    }

    const key = token.slice(2);
    const value = argv[index + 1];
    args[key] = value;
    index += 1;
  }

  return args;
}

async function loadSpec(specPath) {
  const resolvedPath = path.resolve(process.cwd(), specPath);
  const rawSpec = await fs.readFile(resolvedPath, "utf8");
  const spec = JSON.parse(rawSpec);
  return {
    resolvedPath,
    spec,
  };
}

async function ensureParentDirectory(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

async function saveFailureScreenshot(
  page,
  outputPath = "../../.artifacts/webapp-qa/failure.png",
) {
  const resolvedOutputPath = path.resolve(process.cwd(), outputPath);
  await ensureParentDirectory(resolvedOutputPath);
  await page.screenshot({
    path: resolvedOutputPath,
    fullPage: true,
  });
  console.error(`Saved failure screenshot to ${resolvedOutputPath}`);
}

async function waitForText(page, text, timeout) {
  await page.waitForFunction(
    (expectedText) => document.body?.innerText.includes(expectedText),
    { timeout },
    text,
  );
}

async function assertText(page, text, timeout) {
  try {
    await waitForText(page, text, timeout);
  } catch (error) {
    const bodyText = await page.evaluate(() => document.body?.innerText || "");
    throw new Error(
      `Expected text not found: "${text}"\nCurrent page text:\n${bodyText}`,
      { cause: error },
    );
  }
}

async function runStep(page, step, defaultTimeout, fallbackOutputPath) {
  const timeout = step.timeout ?? defaultTimeout;

  switch (step.action) {
    case "goto":
      await page.goto(step.url, {
        waitUntil: step.waitUntil ?? "networkidle2",
        timeout,
      });
      return;

    case "waitForSelector":
      await page.waitForSelector(step.selector, {
        timeout,
        visible: step.visible ?? true,
      });
      return;

    case "waitForText":
      await waitForText(page, step.text, timeout);
      return;

    case "click":
      await page.waitForSelector(step.selector, {
        timeout,
        visible: true,
      });
      await page.click(step.selector);
      return;

    case "type":
      await page.waitForSelector(step.selector, {
        timeout,
        visible: true,
      });
      await page.click(step.selector, { clickCount: 3 });
      if (step.clear ?? true) {
        await page.keyboard.press("Backspace");
      }
      await page.type(step.selector, step.text, {
        delay: step.delay ?? 20,
      });
      return;

    case "press":
      await page.keyboard.press(step.key);
      return;

    case "hover":
      await page.waitForSelector(step.selector, {
        timeout,
        visible: true,
      });
      await page.hover(step.selector);
      return;

    case "assertSelector":
      await page.waitForSelector(step.selector, {
        timeout,
        visible: step.visible ?? true,
      });
      return;

    case "assertText":
      await assertText(page, step.text, timeout);
      return;

    case "assertUrlIncludes":
      await page.waitForFunction(
        (expectedFragment) => window.location.href.includes(expectedFragment),
        { timeout },
        step.value,
      );
      return;

    case "waitForTimeout":
      await new Promise((resolve) => {
        setTimeout(resolve, step.timeout ?? 500);
      });
      return;

    case "screenshot": {
      const outputPath = path.resolve(
        process.cwd(),
        step.outputPath ?? fallbackOutputPath,
      );
      await ensureParentDirectory(outputPath);
      await page.screenshot({
        path: outputPath,
        fullPage: step.fullPage ?? true,
      });
      console.log(`Saved screenshot to ${outputPath}`);
      return;
    }

    default:
      throw new Error(`Unsupported step action: ${step.action}`);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.spec) {
    throw new Error("Usage: npm run check -- --spec <path-to-spec.json>");
  }

  const { resolvedPath, spec } = await loadSpec(args.spec);
  const launchOptions = {
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
    headless: spec.headless ?? true,
  };

  if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    launchOptions.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
  }

  if (spec.launchArgs?.length) {
    launchOptions.args = [...launchOptions.args, ...spec.launchArgs];
  }

  const browser = await puppeteer.launch(launchOptions);

  try {
    const page = await browser.newPage();
    const viewport = spec.viewport ?? { width: 1440, height: 960 };
    const timeout = spec.timeout ?? 15000;
    const outputPath = spec.outputPath ?? "./.artifacts/webapp-qa/latest.png";

    await page.setViewport(viewport);
    page.setDefaultTimeout(timeout);
    page.on("console", (message) => {
      console.log(`[browser:${message.type()}] ${message.text()}`);
    });
    page.on("pageerror", (error) => {
      console.error(`[browser:pageerror] ${error.message}`);
    });
    page.on("requestfailed", (request) => {
      console.error(
        `[browser:requestfailed] ${request.method()} ${request.url()} ${request.failure()?.errorText || ""}`,
      );
    });

    if (spec.url) {
      await page.goto(spec.url, {
        waitUntil: spec.waitUntil ?? "networkidle2",
        timeout,
      });
    }

    for (const step of spec.steps ?? []) {
      await runStep(page, step, timeout, outputPath);
    }

    if (!spec.steps?.some((step) => step.action === "screenshot")) {
      const resolvedOutputPath = path.resolve(process.cwd(), outputPath);
      await ensureParentDirectory(resolvedOutputPath);
      await page.screenshot({
        path: resolvedOutputPath,
        fullPage: true,
      });
      console.log(`Saved screenshot to ${resolvedOutputPath}`);
    }

    console.log(`Completed spec ${resolvedPath}`);
  } catch (error) {
    const pages = await browser.pages();
    const page = pages.at(-1);

    if (page) {
      await saveFailureScreenshot(page);
    }

    throw error;
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exit(1);
});
