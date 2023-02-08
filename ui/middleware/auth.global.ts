export default defineNuxtRouteMiddleware((to) => {
  const user = useSupabaseUser();
  if (!user.value && to.name !== "login") {
    return navigateTo("/login");
  } else if (user.value && to.name === "login") {
    return navigateTo("/");
  }
});
