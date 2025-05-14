/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "i2c.h"
#include "usart.h"
#include "spi.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include "icm20948.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
axises my_gyro;
axises my_accel;
axises my_mag;
uint32_t adc_values[3]; // for9hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
#ifdef __GNUC__
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

PUTCHAR_PROTOTYPE {
    HAL_UART_Transmit(&hlpuart1, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
    HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
    return ch;
}
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_LPUART1_UART_Init();
  MX_SPI1_Init();
  MX_USART2_UART_Init();
  MX_ADC_Init();
  /* USER CODE BEGIN 2 */
//   icm20948_init();
//    ak09916_init();
  uint8_t data[] = "Initializing\n\r"; // Define the string to be sent
  	  HAL_UART_Transmit(&hlpuart1, data, sizeof(data), HAL_MAX_DELAY); // Send the string

  	printf("Setting scale factor to _250dps and _2g");
//  	icm20948_gyro_full_scale_select(_250dps);
//  	icm20948_accel_full_scale_select(_2g);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  uint8_t TX_Buffer [] = "A" ;

//	  HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_1);
	  HAL_SPI_Transmit(&hspi1, TX_Buffer, 1, 1000); //Sending in Blocking mode
//	  HAL_Delay(1000);


	  HAL_ADC_Start(&hadc);

	 		   // Wait for all conversions to complete
	 		   for (int i = 0; i < 3; i++) {
	 		     // Wait for conversion to complete
	 		     HAL_ADC_PollForConversion(&hadc, 100);

	 		     // Get the ADC value for current channel
	 		     adc_values[i] = HAL_ADC_GetValue(&hadc);
	 		   }

	 		   HAL_ADC_Stop(&hadc);

	 		   // Display results as you were doing before
//	 		   HAL_UART_Transmit(&hlpuart1, "a", 1, HAL_MAX_DELAY);
	 		   for (int i = 0; i < 3; i++) {
	 			  printf("F%d:%lu\r\n", i, adc_values[i]);
	 		     uint8_t Test[7]; // Enough for 4 digits + \n\r\0
//	 		     itoa(adc_values[i], (char*)Test, 10);
//	 		     Test[4] = '\n';
//	 		     Test[5] = '\r';
//	 		     Test[6] = '\0';
//	 		     printf((char*)i);
//	 		     printf(":");
//	 		     printf("\n\r");
//	 		     printf((char*)Test);
//	 		     HAL_UART_Transmit(&hlpuart1, Test, sizeof(Test), HAL_MAX_DELAY);
//	 		     HAL_UART_Transmit(&huart2, Test, sizeof(Test), HAL_MAX_DELAY);
	 		     // Small delay between values
	 		   }

	 		  HAL_Delay(50);
//	  HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_1);
//	  HAL_Delay(1000); // Wait for 1 second before sending again
//	  printf("Hello World\n\r");

//	  icm20948_gyro_read(&my_gyro);
//	  icm20948_accel_read(&my_accel);
//	  ak09916_mag_read(&my_mag);
//
//
//
//	  printf("G: X=%d, Y=%d, Z=%d\r\n", (int)my_gyro.x, (int)my_gyro.y, (int)my_gyro.z);
//	  printf("A: X=%d, Y=%d, Z=%d\r\n", (int)my_accel.x, (int)my_accel.y, (int)my_accel.z);
//	  printf("M: X=%d, Y=%d, Z=%d\r\n", (int)my_mag.x, (int)my_mag.y, (int)my_mag.z);
	  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_7);
//	  HAL_Delay(1);
//	  delay_us(30);
//	  HAL_GPIO_TogglePin(LD2_GPIO_Port,LD2_Pin);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLLMUL_4;
  RCC_OscInitStruct.PLL.PLLDIV = RCC_PLLDIV_2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART2|RCC_PERIPHCLK_LPUART1
                              |RCC_PERIPHCLK_I2C1;
  PeriphClkInit.Usart2ClockSelection = RCC_USART2CLKSOURCE_PCLK1;
  PeriphClkInit.Lpuart1ClockSelection = RCC_LPUART1CLKSOURCE_PCLK1;
  PeriphClkInit.I2c1ClockSelection = RCC_I2C1CLKSOURCE_PCLK1;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
