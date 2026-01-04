# If we reach here, try XPath as a last resort
        if time.time() <= end_time:
            for language_keyword in REVIEW_WORDS:
                try:
                    # Try XPath contains text
                    xpath = f"//*[contains(text(), '{language_keyword}')]"
                    elements = driver.find_elements(By.XPATH, xpath)

                    for element in elements:
                        try:
                            log.info(f"Trying XPath with keyword '{language_keyword}'")
                            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                            time.sleep(0.7)
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(1.5)

                            if self.verify_reviews_tab_clicked(driver):
                                log.info(f"Successfully clicked element with keyword '{language_keyword}'")
                                return True
                        except:
                            continue
                except:
                    continue

# Final attempt: try to navigate directly to reviews by URL
        try:
            current_url = driver.current_url
            if "?hl=" in current_url:  # Preserve language setting if present
                lang_param = re.search(r'\?hl=([^&]*)', current_url)
                if lang_param:
                    lang_code = lang_param.group(1)
                    # Try to replace the current part with 'reviews' or append it
                    if '/place/' in current_url:
                        parts = current_url.split('/place/')
                        new_url = f"{parts[0]}/place/{parts[1].split('/')[0]}/reviews?hl={lang_code}"
                        driver.get(new_url)
                        time.sleep(2)
                        if "review" in driver.current_url.lower():
                            log.info("Navigated directly to reviews page via URL")
                            return True

            # Try to identify reviews link in URL
            if '/place/' in current_url and '/reviews' not in current_url:
                parts = current_url.split('/place/')
                new_url = f"{parts[0]}/place/{parts[1].split('/')[0]}/reviews"
                driver.get(new_url)
                time.sleep(2)
                if "review" in driver.current_url.lower():
                    log.info("Navigated directly to reviews page via URL")
                    return True
        except Exception as url_error:
            log.warning(f"Failed to navigate to reviews via URL: {url_error}")

Lignes 440