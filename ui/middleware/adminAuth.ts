export default defineNuxtRouteMiddleware(() => {
  const user = useSupabaseUser();
  const validEmails = ["stevenjpx2@gmail.com"];
  if (user.value === null || !validEmails.includes(user.value.email ?? "")) {
    return navigateTo("/login");
  }
});
