import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "../components/ProtectedRoute";
import CompanyProfile from "../pages/Company/CompanyProfile";
import JobsList from "../pages/Company/JobsList";
import Applications from "../pages/Company/Applications";

const companyRoutesConfig = [
   { path: "profile", element: <CompanyProfile /> },
   { path: "jobs", element: <JobsList /> },
   { path: "jobs/applications/:jobID", element: <Applications /> },
];

const CompanyRoutes = () => {
   return (
      <Routes>
         {companyRoutesConfig.map((route, index) => (
            <Route
               key={index}
               path={route.path}
               element={
                  <ProtectedRoute
                     element={route.element}
                     requiredRole={"company"}
                  />
               }
            />
         ))}
      </Routes>
   );
};

export default CompanyRoutes;
