<script setup lang="ts">
const router = useRouter();
const user = useSupabaseUser();
const client = useSupabaseAuthClient();

const signOut = async () => {
  await client.auth.signOut();
  router.push("/login");
};
</script>

<template>
  <div>
    <nav class="bg-white w-full fixed top-0 border-b border-slate-400 py-5">
      <div class="container flex gap-5 mx-auto items-center">
        <nuxt-link to="/">Home</nuxt-link>
        <nuxt-link to="/admin">Admin Panel</nuxt-link>
        <button
          v-if="user"
          @click="signOut()"
          class="btn bg-red-600 text-white hover:bg-red-700 ml-auto"
        >
          Logout
        </button>
      </div>
    </nav>
    <main class="container mt-24 mx-auto">
      <slot />
    </main>
  </div>
</template>
