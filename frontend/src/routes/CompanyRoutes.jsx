import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "../components/ProtectedRoute";
import CompanyProfile from "../pages/Company/CompanyProfile";
import JobsList from "../pages/Company/JobsList";
import Applications from "../pages/Company/Applications";

const CompanyRoutes = () => {
   return (
      <Routes>
         <Route
            path="profile"
            element={<ProtectedRoute element={<CompanyProfile />} requiredRole="company" />}
         />
         <Route 
            path="jobs" 
            element={<ProtectedRoute element={<JobsList />} requiredRole="company" />} 
         />
         <Route
            path="jobs/applications/:jobId"
            element={<ProtectedRoute element={<Applications />} requiredRole="company" />}
         />
      </Routes>
   );
};

export default CompanyRoutes;
