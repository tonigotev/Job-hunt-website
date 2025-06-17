import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "./_axiosInstance";

// --------------------
// API Functions
// --------------------

const fetchMyCompany = async () => {
   const response = await axiosInstance.get("companies/my-company/");
   return response.data;
};

const updateMyCompany = async (companyData) => {
   const response = await axiosInstance.patch(
      "companies/my-company/",
      companyData
   );
   return response.data;
};

// --------------------
// Custom Hooks
// --------------------

const useFetchMyCompanyQuery = () => {
   return useQuery({
      queryKey: ["myCompany"],
      queryFn: fetchMyCompany,
      staleTime: 5 * 60 * 1000,
   });
};

const useUpdateCompanyMutation = () => {
   const queryClient = useQueryClient();

   return useMutation({
      mutationFn: updateMyCompany,
      onSuccess: (data) => {
         queryClient.invalidateQueries({ queryKey: ["myCompany"] });
         console.log("Company updated successfully:", data);
      },
      onError: (error) => {
         console.error("Error updating company:", error);
      },
   });
};

export {
   useFetchMyCompanyQuery,
   useUpdateCompanyMutation,
};
