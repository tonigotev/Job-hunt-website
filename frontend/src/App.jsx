import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
// import Home from "./pages/Home";
import NavBar from "./components/NavBar";
import Register from "./pages/Register";
import LoginForm from "./pages/Login";
import AdminRoutes from "./routes/AdminRoutes";
import CompanyRoutes from "./routes/CompanyRoutes";
import JobSeekerRoutes from "./routes/JobSeekerRoutes";
import JobDetails from "./pages/JobDetails";
import Home from "./pages/JobSeeker/Home";

function App() {
   return (
      <AuthProvider>
         <BrowserRouter>
            <ConditionalNavBar>
               <Routes>
                  <Route path="/register" element={<Register />} />
                  <Route path="/login" element={<LoginForm />} />
                  {/* <Route path="/" element={<Home />} /> */}
                  <Route path="/" element={<Home />} />
                  <Route path="admin/*" element={<AdminRoutes />} />
                  <Route path="company/*" element={<CompanyRoutes />} />
                  <Route path="job_seeker/*" element={<JobSeekerRoutes />} />
                  <Route path="/job/:jobId" element={<JobDetails />} />
               </Routes>
            </ConditionalNavBar>
         </BrowserRouter>
      </AuthProvider>
   );
}

function ConditionalNavBar({ children }) {
   const location = useLocation();
   const hideNavBarRoutes = ["/register", "/login"];

   return (
      <>
         {!hideNavBarRoutes.includes(location.pathname) && <NavBar />}
         {children}
      </>
   );
}

export default App;
