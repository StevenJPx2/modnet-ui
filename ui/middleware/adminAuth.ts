export default defineNuxtRouteMiddleware(() => {
  const user = useSupabaseUser();
  if (user.value === null || !validEmails.includes(user.value.email ?? "")) {
    return navigateTo("/login");
  }
});
