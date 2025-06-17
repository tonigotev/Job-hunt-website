import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

const ResetPassword = () => {
   const [password, setPassword] = useState("");
   const [confirmPassword, setConfirmPassword] = useState("");
   const [searchParams] = useSearchParams();
   const navigate = useNavigate();
   const [message, setMessage] = useState("");
   const [error, setError] = useState("");

   const uid = searchParams.get("uid");
   const token = searchParams.get("token");

   const handleSubmit = async (e) => {
      e.preventDefault();
      if (password !== confirmPassword) {
         setError("Passwords don't match!");
         return;
      }
      setError("");
      setMessage("");

      try {
         await axios.post(
            `${
               import.meta.env.VITE_API_URL
            }/auth/users/reset_password_confirm/`,
            { uid, token, new_password: password }
         );
         setMessage("Your password has been reset successfully. You can now log in.");
         setTimeout(() => {
            navigate("/login");
         }, 3000);
      } catch (err) {
         setError("Failed to reset password. The link may be invalid or expired.");
         console.error(err);
      }
   };

   return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
         <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-center text-gray-900">
               Reset Your Password
            </h2>
            {message && (
               <div className="p-4 text-sm text-green-700 bg-green-100 border-l-4 border-green-500">
                  {message}
               </div>
            )}
            {error && (
               <div className="p-4 text-sm text-red-700 bg-red-100 border-l-4 border-red-500">
                  {error}
               </div>
            )}
            <form className="space-y-6" onSubmit={handleSubmit}>
               <div>
                  <label
                     htmlFor="password"
                     className="block text-sm font-medium text-gray-700"
                  >
                     New Password
                  </label>
                  <div className="mt-1">
                     <input
                        id="password"
                        name="password"
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                     />
                  </div>
               </div>
               <div>
                  <label
                     htmlFor="confirm-password"
                     className="block text-sm font-medium text-gray-700"
                  >
                     Confirm New Password
                  </label>
                  <div className="mt-1">
                     <input
                        id="confirm-password"
                        name="confirm-password"
                        type="password"
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                     />
                  </div>
               </div>

               <div>
                  <button
                     type="submit"
                     className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                     Reset Password
                  </button>
               </div>
            </form>
         </div>
      </div>
   );
};

export default ResetPassword; 