<template>
  <nuxt-layout>
    <nuxt-page />
  </nuxt-layout>
</template>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&display=swap");

html {
  font-family: "Inter";
}

.container-full {
  @apply container;
  @apply mx-auto;
  @apply px-2;
}

.btn {
  @apply px-4;
  @apply py-2;
  @apply border;
  @apply rounded;

  &-lg {
    @apply px-5;
    @apply py-4;
  }
}
</style>
