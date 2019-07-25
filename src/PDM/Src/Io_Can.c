/*****************************************************************************
 * Includes
 ******************************************************************************/
#include "Io_Can.h"

/******************************************************************************
 * Module Preprocessor Constants
 ******************************************************************************/

/******************************************************************************
 * Module Preprocessor Macros
 ******************************************************************************/

/******************************************************************************
 * Module Typedefs
 ******************************************************************************/

/******************************************************************************
 * Module Variable Definitions
 ******************************************************************************/
// clang-format off
static CanMaskFilterConfig_Struct mask_filters[] =
{
    INIT_MASK_FILTER(MASKMODE_16BIT_ID_BMS, MASKMODE_16BIT_MASK_BMS),
    INIT_MASK_FILTER(MASKMODE_16BIT_ID_SHARED, MASKMODE_16BIT_MASK_SHARED)
};
// clang-format on

/******************************************************************************
 * Private Function Prototypes
 ******************************************************************************/

/******************************************************************************
 * Private Function Definitions
 ******************************************************************************/

/******************************************************************************
 * Function Definitions
 ******************************************************************************/
CanMaskFilterConfig_Struct *Io_Can_GetCanMaskFilters(void)
{
    return mask_filters;
}
