import { useState } from "react";
import axios from "axios";

const ForgotPassword = () => {
   const [email, setEmail] = useState("");
   const [message, setMessage] = useState("");
   const [error, setError] = useState("");

   const handleSubmit = async (e) => {
      e.preventDefault();
      setMessage("");
      setError("");
      try {
         const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/auth/users/reset_password/`,
            { email }
         );
         setMessage(
            "If an account with that email exists, a password reset link has been sent."
         );
      } catch (err) {
         setError("An error occurred. Please try again.");
         console.error(err);
      }
   };

   return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
         <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-center text-gray-900">
               Forgot Your Password?
            </h2>
            <p className="text-center text-gray-600">
               Enter your email address and we will send you a link to reset your
               password.
            </p>
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
                     htmlFor="email"
                     className="block text-sm font-medium text-gray-700"
                  >
                     Email address
                  </label>
                  <div className="mt-1">
                     <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                     />
                  </div>
               </div>

               <div>
                  <button
                     type="submit"
                     className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                     Send Reset Link
                  </button>
               </div>
            </form>
         </div>
      </div>
   );
};

export default ForgotPassword; 