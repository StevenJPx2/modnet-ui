// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: { head: { title: "MODNet UI | Steven John" } },
  modules: [
    "nuxt-icon",
    "@nuxtjs/fontaine",
    "@nuxtjs/tailwindcss",
    "@vueuse/nuxt",
    "@nuxtjs/supabase",
  ],
});
