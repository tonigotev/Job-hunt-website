import axios from "axios";
import { QueryClient } from "@tanstack/react-query";

const axiosInstance = axios.create({
   baseURL: "/api/",
   headers: {
      "Content-Type": "application/json",
   },
});

// NEW: Attach the stored access token (if it exists) to every request by default
// This ensures the user remains authenticated after a page refresh.
const persistedAccessToken = localStorage.getItem("access_token");
if (persistedAccessToken) {
   axiosInstance.defaults.headers.common[
      "Authorization"
   ] = `Bearer ${persistedAccessToken}`;
}

const queryClient = new QueryClient();

axiosInstance.interceptors.response.use(
   (response) => response,
   async (error) => {
      const originalRequest = error.config;

      if (originalRequest.skipInterceptor) {
         return Promise.reject(error);
      }

      if (error.response.status === 401 && !originalRequest._retry) {
         originalRequest._retry = true;

         const refreshToken = localStorage.getItem("refresh_token");
         if (!refreshToken) {
            window.location.href = "/login";
            return Promise.reject(error);
         }

         try {
            console.log("Token Refreshing...");

            const response = await axios.post(
               "/api/auth/token/refresh/",
               { refresh: refreshToken }
            );

            const { access, refresh } = response.data;

            localStorage.setItem("access_token", access);
            localStorage.setItem("refresh_token", refresh);

            axiosInstance.defaults.headers.common[
               "Authorization"
            ] = `Bearer ${access}`;

            originalRequest.headers["Authorization"] = `Bearer ${access}`;

            return axiosInstance(originalRequest);
         } catch (refreshError) {
            console.error("Refresh token is expired", refreshError);
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login";
            return Promise.reject(refreshError);
         }
      }
      return Promise.reject(error);
   }
);

export { axiosInstance, queryClient };
