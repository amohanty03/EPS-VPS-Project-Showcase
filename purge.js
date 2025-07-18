import { PurgeCSS } from "purgecss";
const purgeCSSResults = await new PurgeCSS().purge({
  content: ["**/*.html"],
  css: ["**/*.css"],
});