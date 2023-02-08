<script setup lang="ts">
const user = useSupabaseUser();
const client = useSupabaseAuthClient();
const router = useRouter();

watch(
  user,
  (val) => {
    if (val) router.push("/");
  },
  { deep: true }
);

// Login method using providers
const login = async (
  provider: "github" | "google" | "gitlab" | "bitbucket"
) => {
  const { error } = await client.auth.signInWithOAuth({
    provider,
    options: { redirectTo: "https://modnet.stevenjohn.co/" },
  });
  if (error) {
    return alert("Something went wrong !");
  }
  router.push("/");
};
</script>

<template>
  <div class="grid w-full h-screen place-content-center">
    <button
      class="btn flex items-center text-lg gap-2"
      @click="login('github')"
    >
      <icon name="simple-icons:github" /> Login with Github
    </button>
  </div>
</template>
